
/**
 * A list of Promises to be executed before the page loader animation becomes hidden
 * 
 * @global
 */
var preLoadedEventList = [
    () => {
        return new Promise((resolve, reject) => {
            // if (window.location.protocol === "file:") return resolve();
            setTimeout(() => resolve(), $_DEFAULTS.PAGE.MINIMUM_INSISTENT_WAIT);
        })
    }
];

/**
 * A list of Promises to be executed AFTER `preLoadedEventList` is completed AND after the page is done loading
 * 
 * @global
 */
var postLoadedEventList = [];