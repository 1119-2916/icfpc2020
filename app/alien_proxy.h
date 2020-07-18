#ifndef ALIEN_PROXY_H
#define ALIEN_PROXY_H

#include <regex>
#include <string>

#include "httplib.h"

class AlienProxyClient {
 public:
  AlienProxyClient(const std::string& apiKey) : apiKey(apiKey), client("icfpc2020-api.testkontur.ru") {}

  std::shared_ptr<httplib::Response> Send(const std::string& body) {
    return client.Post(("/aliens/send?apiKey=" + apiKey).c_str(), body.c_str(), "text/plain");
  }

 private:
  std::string apiKey;
  httplib::Client client;
};

#endif  // ALIEN_PROXY_H
