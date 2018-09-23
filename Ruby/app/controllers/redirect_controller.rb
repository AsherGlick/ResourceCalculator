require 'net/http'
require 'uri'
class RedirectController < ApplicationController
  def index

    # Grab the redirected URL
    url = URI.parse('https://goo.gl/'+params[:shorturl])
    req = Net::HTTP::Get.new(url.request_uri)
    http = Net::HTTP.new(url.host, url.port)
    http.use_ssl = (url.scheme == "https")
    res = http.request(req)

    if res['location'] == nil
      raise ActionController::RoutingError.new('Not Found')
    end

    # If the redirect is to a resourcecalculator link then redirect, or 404
    if (res['location'].start_with?('https://resourcecalculator.com'))
      url = res['location']
    else
      raise ActionController::RoutingError.new('Not Found')
    end

    # Redirect
    redirect_to url
  end
end
