#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "Ws2_32.lib")
#else
    #include <sys/socket.h>
    #include <arpa/inet.h>
    #include <unistd.h>
#endif

const int PORT = 8080;
const int BUFFER_SIZE = 1024;

class Game {
public:
    int bird_y;
    int pipe_x, pipe_gap_y;
    int score;
    bool gameOver;

    Game() {
        reset();
    }

    void reset() {
        bird_y = 10;
        pipe_x = 40;
        pipe_gap_y = 10;
        score = 0;
        gameOver = false;
    }

    void updateGameState() {
        bird_y++;
        pipe_x--;
        if (pipe_x < 0) {
            pipe_x = 40;
            pipe_gap_y = rand() % 10 + 5;
            score++;
        }
        if (bird_y > 20) {
            gameOver = true;
        }
    }

    std::string getState() {
        return std::to_string(bird_y) + " " + std::to_string(pipe_x) + " " + std::to_string(pipe_gap_y) + " " + std::to_string(score);
    }

    int getReward() {
        if (gameOver) {
            return -100;  // Negative reward for game over
        }
        return 1;  // Positive reward for surviving
    }
};

int main() {
#ifdef _WIN32
    WSADATA wsaData;
    int wsaStartupResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (wsaStartupResult != 0) {
        std::cerr << "WSAStartup failed: " << wsaStartupResult << std::endl;
        return 1;
    }
#endif

    int server_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

#ifdef _WIN32
    server_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_fd == INVALID_SOCKET) {
        std::cerr << "Socket failed: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }
#else
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return 1;
    }
#endif

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

#ifdef _WIN32
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
        std::cerr << "Bind failed: " << WSAGetLastError() << std::endl;
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
#else
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        std::cerr << "Bind failed" << std::endl;
        return 1;
    }
#endif

#ifdef _WIN32
    if (listen(server_fd, 3) == SOCKET_ERROR) {
        std::cerr << "Listen failed: " << WSAGetLastError() << std::endl;
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
#else
    if (listen(server_fd, 3) < 0) {
        std::cerr << "Listen failed" << std::endl;
        return 1;
    }
#endif

    std::cout << "Waiting for Python script connection..." << std::endl;

    int new_socket;
#ifdef _WIN32
    new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen);
    if (new_socket == INVALID_SOCKET) {
        std::cerr << "Accept failed: " << WSAGetLastError() << std::endl;
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
#else
    new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
    if (new_socket < 0) {
        std::cerr << "Accept failed" << std::endl;
        return 1;
    }
#endif

    std::cout << "Connection established." << std::endl;

    Game game;
    char buffer[BUFFER_SIZE] = {0};

    while (true) {
        // Clear buffer
        memset(buffer, 0, BUFFER_SIZE);

        // Receive message from the Python client
#ifdef _WIN32
        int valread = recv(new_socket, buffer, BUFFER_SIZE, 0);
#else
        int valread = read(new_socket, buffer, BUFFER_SIZE);
#endif

        std::string response(buffer);

        // Check if the Python client sent a "reset" command
        if (response == "reset") {
            game.reset();  // Reset the game state
            std::string initial_state = game.getState();  // Get initial state
            send(new_socket, initial_state.c_str(), initial_state.size(), 0);  // Send initial state back to Python
            continue;  // Continue to next iteration to wait for more messages
        }

        // Normal game progression (handle actions like "ping" for flap or "no_ping" for no flap)
        if (response == "ping") {
            game.updateGameState();
        }

        // Send the current game state and reward to the Python client
        std::string gameState = game.getState();
        int reward = game.getReward();
        std::string message = gameState + " " + std::to_string(reward);
#ifdef _WIN32
        send(new_socket, message.c_str(), message.size(), 0);
#else
        send(new_socket, message.c_str(), message.size(), 0);
#endif

        // Check if the game is over
        if (game.gameOver) {
            std::cout << "Game Over. Restarting game..." << std::endl;
            game.reset();
        }
    }

#ifdef _WIN32
    closesocket(new_socket);
    closesocket(server_fd);
    WSACleanup();
#else
    close(new_socket);
    close(server_fd);
#endif

    return 0;
}
