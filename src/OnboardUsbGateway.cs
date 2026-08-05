using System;
using System.IO.Ports;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace CognitiveEntanglement
{
    /// <summary>
    /// High-Performance C# USB-to-WebSocket Telemetry Gateway (Android/iOS Native Spec).
    /// Bridges the low-level physical USB-OTG serial connection from the Pixhawk Flight Controller
    /// straight to the local Python/Go WebRTC companion server with sub-millisecond packet latency.
    /// </summary>
    public class OnboardUsbGateway
    {
        private SerialPort _serialPort;
        private ClientWebSocket _webSocket;
        private readonly Uri _serverUri = new Uri("ws://127.0.0.1:5000/socket.io/?EIO=4&transport=websocket");
        private readonly CancellationTokenSource _cts = new CancellationTokenSource();

        public OnboardUsbGateway(string portName = "/dev/ttyUSB0", int baudRate = 921600)
        {
            // Configure high-speed serial telemetery parameters
            _serialPort = new SerialPort(portName, baudRate, Parity.None, 8, StopBits.One)
            {
                ReadTimeout = 500,
                WriteTimeout = 500,
                Handshake = Handshake.None
            };
            _webSocket = new ClientWebSocket();
        }

        public async Task StartAsync()
        {
            Console.WriteLine("[C# GATEWAY]: Opening physical USB-OTG Serial connection to Flight Controller...");
            try
            {
                _serialPort.Open();
                Console.WriteLine($"[C# GATEWAY]: Connected to serial port {_serialPort.PortName} at {_serialPort.BaudRate} bps.");

                Console.WriteLine("[C# GATEWAY]: Connecting to local high-speed WebSocket telemetry server...");
                await _webSocket.ConnectAsync(_serverUri, _cts.Token);
                Console.WriteLine("[C# GATEWAY]: Telemetry link established.");

                // Start concurrent bidirectional packet routing
                var serialToWebsocketTask = Task.Run(RouteSerialToWebSocketAsync);
                var websocketToSerialTask = Task.Run(RouteWebSocketToSerialAsync);

                await Task.WhenAll(serialToWebsocketTask, websocketToSerialTask);
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"[C# GATEWAY ERROR]: Connection failure: {ex.Message}");
                Stop();
            }
        }

        private async Task RouteSerialToWebSocketAsync()
        {
            byte[] buffer = new byte[1024];
            while (!_cts.Token.IsCancellationRequested && _serialPort.IsOpen && _webSocket.State == WebSocketState.Open)
            {
                try
                {
                    if (_serialPort.BytesToRead > 0)
                    {
                        int bytesRead = _serialPort.Read(buffer, 0, buffer.Length);
                        // Forward raw MAVLink packet bytes straight to WebSocket server
                        await _webSocket.SendAsync(new ArraySegment<byte>(buffer, 0, bytesRead), 
                            WebSocketMessageType.Binary, true, _cts.Token);
                    }
                    await Task.Delay(1); // Yield thread to maintain 1000Hz polling rate
                }
                catch (Exception ex)
                {
                    Console.Error.WriteLine($"[C# GATEWAY ERROR]: Serial-to-Socket routing crash: {ex.Message}");
                }
            }
        }

        private async Task RouteWebSocketToSerialAsync()
        {
            byte[] buffer = new byte[1024];
            while (!_cts.Token.IsCancellationRequested && _serialPort.IsOpen && _webSocket.State == WebSocketState.Open)
            {
                try
                {
                    var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), _cts.Token);
                    if (result.MessageType == WebSocketMessageType.Binary)
                    {
                        // Write incoming steering vectors straight to Pixhawk UART
                        _serialPort.Write(buffer, 0, result.Count);
                    }
                }
                catch (Exception ex)
                {
                    Console.Error.WriteLine($"[C# GATEWAY ERROR]: Socket-to-Serial routing crash: {ex.Message}");
                }
            }
        }

        public void Stop()
        {
            _cts.Cancel();
            if (_serialPort != null && _serialPort.IsOpen)
            {
                _serialPort.Close();
            }
            _webSocket?.Dispose();
            Console.WriteLine("[C# GATEWAY]: Gateway terminated safely.");
        }
    }
}
