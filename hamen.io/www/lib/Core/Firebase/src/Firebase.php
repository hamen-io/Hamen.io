<?php

namespace Hamen\Core\Firebase\Internal;


class Firebase {
    private $apiKey;
    private $authDomain;
    private $databaseURL;
    private $projectID;
    private $storageBucket;
    private $messagingSenderID;
    private $appID;
    private $secretKey;

    function __construct($apiKey, $authDomain, $databaseURL, $projectID, $storageBucket, $messagingSenderID, $appID, $secretKey) {
        $this->apiKey = $apiKey;
        $this->authDomain = $authDomain;
        $this->databaseURL = $databaseURL;
        $this->projectID = $projectID;
        $this->storageBucket = $storageBucket;
        $this->messagingSenderID = $messagingSenderID;
        $this->appID = $appID;
        $this->secretKey = $secretKey;
    }

    function ok(): bool {
        return true;
    }
    
    function get(...$path) {
        $dataUrl = $this->databaseURL . "/" . join($path, "/") . ".json?auth=" . $this->secretKey;
    
        $ch = curl_init($dataUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $result = curl_exec($ch);
        curl_close($ch);
    
        return json_decode($result, true);
    }

    function set($value, ...$path) {
        $dataUrl = $this->databaseURL . "/" . join($path, "/") . ".json?auth=" . $this->secretKey;

        $ch = curl_init($dataUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($value));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $result = curl_exec($ch);
        curl_close($ch);

        return json_decode($result, true);
    }

    function remove(...$path) {
        $dataUrl = $this->databaseURL . "/" . join($path, "/") . ".json?auth=" . $this->secretKey;

        $ch = curl_init($dataUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $result = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
    }
};