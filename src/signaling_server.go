package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"github.com/gorilla/websocket"
)

// Go High-Speed WebRTC Signaling & Telemetry Server (Aerospatial Spec).
// Implemented in Go (Golang) to utilize lightweight Goroutines and 
// mutex-locked concurrent map matrices for ultra-low latency packet routing.
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow all cross-origins for 5G cellular phone pairing
	},
}

type Client struct {
	conn *websocket.Conn
	role string // PILOT (Phone B) or DRONE (Phone A)
}

var (
	clients    = make(map[*Client]bool)
	clientsMu  sync.Mutex
)

func handleConnections(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("[GO SIGNALING ERROR]: Handshake failed: %v", err)
		return
	}
	
	client := &Client{conn: ws, role: "UNASSIGNED"}
	
	clientsMu.Lock()
	clients[client] = true
	clientsMu.Unlock()
	
	log.Printf("[GO SIGNALING]: New cellular telemetry link connected: %v", ws.RemoteAddr())

	for {
		var msg map[string]interface{}
		err := ws.ReadJSON(&msg)
		if err != nil {
			log.Printf("[GO SIGNALING]: Connection closed by endpoint: %v", ws.RemoteAddr())
			clientsMu.Lock()
			delete(clients, client)
			clientsMu.Unlock()
			break
		}

		// Parse peer roles and route low-latency packets
		roleVal, ok := msg["role"].(string)
		if ok {
			client.role = roleVal
		}

		// Broadcast WebRTC SDP offers/answers and ICE candidates to opposite peers
		broadcastSignaling(client, msg)
	}
}

func broadcastSignaling(sender *Client, msg map[string]interface{}) {
	clientsMu.Lock()
	defer clientsMu.Unlock()

	for client := range clients {
		if client != sender && (client.role != sender.role || client.role == "UNASSIGNED") {
			err := client.conn.WriteJSON(msg)
			if err != nil {
				log.Printf("[GO SIGNALING ERROR]: Broadcast failed: %v", err)
				client.conn.Close()
				delete(clients, client)
			}
		}
	}
}

func main() {
	fmt.Println("Cognitive Entanglement - Go High-Speed Signaling Core Active.")
	http.HandleFunc("/ws", handleConnections)
	
	log.Fatal(http.ListenAndServe(":5001", nil))
}
