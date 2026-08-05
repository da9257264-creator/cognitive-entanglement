# ==============================================================================
# Cognitive Entanglement - Unified Aerospace Flight Stack Build Automation Makefile 🛠️🛸
# Target: GNU Make
# ==============================================================================

CC = gcc
CXX = g++
CXXFLAGS = -O3 -std=c++17 -fPIC
RUSTC = rustc
GOC = go
CSC = mcs
ASM = as # GNU Assembler

# Build Output Directories
BIN_DIR = bin
SRC_DIR = src

.PHONY: all clean test deploy_pi

all: $(BIN_DIR)/failsafe_watchdog $(BIN_DIR)/signaling_server $(BIN_DIR)/OnboardUsbGateway.exe $(BIN_DIR)/libcoord_transformer.so $(BIN_DIR)/vector_multiply.o

# 1. Compile Rust Safety-Critical Watchdog
$(BIN_DIR)/failsafe_watchdog: $(SRC_DIR)/failsafe_watchdog.rs
	@mkdir -p $(BIN_DIR)
	@echo "Compiling High-Integrity Onboard Watchdog (Rust)..."
	$(RUSTC) -O $< --out-dir $(BIN_DIR)/

# 2. Compile Go Low-Latency Signaling Server
$(BIN_DIR)/signaling_server: $(SRC_DIR)/signaling_server.go
	@mkdir -p $(BIN_DIR)
	@echo "Compiling High-Speed Signaling Core (Go)..."
	@if command -v $(GOC) &> /dev/null; then \
		$(GOC) build -o $@ $<; \
	else \
		echo "Go compiler not found. Skipping Go build."; \
	fi

# 3. Compile C# Onboard USB-to-Socket Gateway
$(BIN_DIR)/OnboardUsbGateway.exe: $(SRC_DIR)/OnboardUsbGateway.cs
	@mkdir -p $(BIN_DIR)
	@echo "Compiling High-Speed Onboard USB Gateway (C#)..."
	@if command -v $(CSC) &> /dev/null; then \
		$(CSC) -out:$@ $<; \
	else \
		echo "Mono C# compiler not found. Skipping C# build."; \
	fi

# 4. Compile Modern C++ Aeronautical Coordinate Frame Transformer
$(BIN_DIR)/libcoord_transformer.so: $(SRC_DIR)/CoordinateTransformer.cpp $(SRC_DIR)/CoordinateTransformer.h
	@mkdir -p $(BIN_DIR)
	@echo "Compiling High-Performance Coordinate Transformer (Modern C++)..."
	$(CXX) $(CXXFLAGS) -shared -o $@ $<

# 5. Compile ARM NEON SIMD Vector Math Optimization (Assembly)
$(BIN_DIR)/vector_multiply.o: $(SRC_DIR)/vector_multiply.S
	@mkdir -p $(BIN_DIR)
	@echo "Assembling ARM NEON SIMD Vector Library (Assembly)..."
	@if [ "$$(uname -m)" = "aarch64" ] || [ "$$(uname -m)" = "arm64" ]; then \
		$(ASM) -o $@ $<; \
	else \
		echo "Non-ARM architecture detected. Skipping hardware-specific ASM compilation."; \
	fi

# 6. Run automated Python/CI test coverage
test:
	@echo "Executing automated unittest verification suite..."
	python3 -m unittest discover -s tests

# 7. Full clean build cleanup
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf $(BIN_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# 8. Raspberry Pi Automated Setup
deploy_pi:
	@echo "Automating Onboard Companion Computer deployment..."
	./deploy.sh
