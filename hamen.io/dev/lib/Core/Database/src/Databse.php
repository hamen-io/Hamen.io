<?php

namespace Hamen\Core\Database\Internal;


class Database {
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

    function update($value, ...$path) {

    }

    function contains(...$path) {
        
    }
    
    function get(...$path) {
    }

    function set($value, ...$path) {
    }

    function remove(...$path) {
    }
};