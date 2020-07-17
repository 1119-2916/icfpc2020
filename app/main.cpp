#include "httplib.h"
#include <iostream>
#include <regex>
#include <string>

int print(const std::shared_ptr<httplib::Response> serverResponse) {
    if(!serverResponse) {
        std::cout << "Unexpected server response:\nNo response from server"
                  << std::endl;
        return 1;
    }

    if(serverResponse->status != 200) {
        std::cout << "Unexpected server response:\nHTTP code: "
                  << serverResponse->status
                  << "\nResponse body: " << serverResponse->body << std::endl;
        return 2;
    }

    std::cout << "Server response: " << serverResponse->body << std::endl;
    return 0;
}

int main(int argc, char *argv[]) {
    const std::string serverUrl(argv[1]);
    const std::string playerKey(argv[2]);

    std::cout << "ServerUrl: " << serverUrl << "; PlayerKey: " << playerKey
              << std::endl;

    const std::regex urlRegexp("http://(.+):(\\d+)");
    std::smatch urlMatches;
    if(!std::regex_search(serverUrl, urlMatches, urlRegexp) ||
       urlMatches.size() != 3) {
        std::cout << "Unexpected server response:\nBad server URL" << std::endl;
        return 1;
    }
    const std::string serverName = urlMatches[1];
    const int serverPort = std::stoi(urlMatches[2]);
    httplib::Client client(serverName, serverPort);
    const std::shared_ptr<httplib::Response> serverResponse1 =
        client.Post(serverUrl.c_str(), playerKey.c_str(), "text/plain");
    const std::shared_ptr<httplib::Response> serverResponse2 = client.Post(
        (serverUrl + "/aliens/send").c_str(), playerKey.c_str(), "text/plain");
    const std::shared_ptr<httplib::Response> serverResponse3 =
        client.Get((serverUrl + "/scoreboard/lightning").c_str());
    const std::shared_ptr<httplib::Response> serverResponse4 =
        client.Get((serverUrl + "/submissions").c_str());
    const std::shared_ptr<httplib::Response> serverResponse5 =
        client.Get((serverUrl + "/submissions").c_str());

    print(serverResponse1);
    print(serverResponse2);
    print(serverResponse3);
    print(serverResponse4);
    print(serverResponse5);

    return 0;
}
