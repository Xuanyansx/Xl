#include <stdio.h>
#include <iostream>
#include <string>
#include <WinSock2.h> // for Windows
// #include <sys/socket.h> // for Linux/Unix



int main(){
    int sockfd, portno, n;
    socklen_t clilen;
    char buffer[256];
    struct sockaddr_in serv_addr, cli_addr;

    // socket create and verification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        std::cout << "ERROR: Could not create socket" << std::endl;
        return 1;
    }
    std::cout << "Socket created successfully" << std::endl;

    // socket binding
    memset((char *) &serv_addr, 0, sizeof(serv_addr));
    portno = 5000;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
        std::cout << "ERROR: Could not bind socket" << std::endl;
        return 1;
    }
    std::cout << "Socket bound successfully" << std::endl;

    // socket listening
    listen(sockfd, 5);
    std::cout << "Socket is listening" << std::endl;

    // socket accepting
    clilen = sizeof(cli_addr);
    int newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0) {
        std::cout << "ERROR: Could not accept connection" << std::endl;
        return 1;
    }
    std::cout << "New connection accepted" << std::endl;

    // socket reading and writing
    std::string message = "Hello from server";
    n = write(newsockfd, message.c_str(), message.length());
    if (n < 0) {
        std::cout << "ERROR: Could not write to socket" << std::endl;
        return 1;
    }
    std::cout << "Message sent successfully" << std::endl;

    n = read(newsockfd, buffer, 256);
    if (n < 0) {
        std::cout << "ERROR: Could not read from socket" << std::endl;
        return 1;
    }
    std::cout << "Message received: " << buffer << std::endl;

    // socket closing
    close(newsockfd);
    std::cout << "Socket closed successfully" << std::endl;
    close(sockfd);
    std::cout << "Socket closed successfully" << std::endl;

    return 0;


}