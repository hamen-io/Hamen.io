/**
 * @global
 * @template T
 */
class State {
    /**
     * @param {T} initialValue The initial value assigned to this state
     */
    constructor(initialValue) {
        this._wrappedValue = initialValue;

        /**
         * @type {((nV: T, oV: T) => void)[]}
         */
        this._listeners = [];
    };

    /**
     * 
     * @param {T} nV 
     */
    setValue(nV) {
        this._listeners.forEach(c => c(nV, this._wrappedValue));
        this._wrappedValue = nV;
    };

    /**
     * 
     * @returns {T}
     */
    getValue() {
        return this._wrappedValue;
    };

    /**
     * Subscribes a callback to be executed when the wrapped value changes
     * 
     * @param {(nV: T, oV: T) => void} callback 
     */
    addListener(onChange) {
        this._listeners.push(onChange);
    };

    /**
     * Unsubscribes a callback from the listener list
     * 
     * @param {(nV: T, oV: T) => void} onChange 
     */
    removeListener(onChange) {
        this._listeners = this._listeners.filter(l => l != onChange);
    };
};

/**
 * @global
*/
class RegistryList {
    constructor() {
        this._values = [];
    }

    register(_) {
        this._values.push(_)
    }

    unregister(_) {
        this._values.filter(c => c != _);
    }

    get values() {
        return this._values
    }
}

/**
 * @global
 */
class SubscriptionList {
    constructor() {
        /**
         * @type {(() => void)[]}
         */
        this._actions = [];
    };

    /**
     * 
     * @param {() => void} callback 
     */
    subscribe(callback) {
        this._actions.push(callback)
    };

    /**
     * 
     * @param {() => void} callback 
     */
    unsubscribe(callback) {
        this._actions = this._actions.filter(c => c != callback);
    };

    trigger(...args) {
        this._actions.forEach(c => c(...args));
    };
};

/**
 * @global
 */
class Identifiable {
    constructor() {
        this.ID = UUID();
    };
};

class Directory {
    /**
     * 
     * @param {string} dirName 
     * @param {{
     *  isProtected: boolean,
     *  parentDirectory: undefined | Directory,
     *  overridePath: undefined | string
     * }} param1 
     */
    constructor(dirName, { isProtected = false, parentDirectory = undefined, overridePath = undefined }) {
        this._dirName = new State(dirName);

        /** @type {undefined | Directory} */
        this.parentDirectory = parentDirectory;

        /** @type {boolean} When true, the directory cannot be deleted */
        this._isProtected = isProtected;

        /** @type {(Directory | File)[]} */
        this._dirContent = [];

        this.overridePath = overridePath;
    };

    /** @param {File} file */
    createFile(file) {
        this._dirContent.push(file);
    };

    /** @param {Directory} directory */
    createDirectory(directory) {
        this._dirContent.push(directory);
    };

    /** @param {File} file */
    removeFile(file) {
        this._dirContent.push(file);
    };

    /** @param {Directory} directory */
    removeDirectory(directory) {
        this._dirContent.push(directory);
    };

    getContents() {
        return this._dirContent;
    };

    /** @returns {boolean} */
    get isProtected() {
        return this._isProtected;
    };

    getPath() {
        return this.overridePath || this.parentDirectory.getPath();
    };
};

class File {
    /**
     * @param {string} fileName 
     * @param {{
     *  isProtected: boolean,
     *  parentDirectory: undefined | Directory
     * }} param1 
     */
    constructor(fileName, { isProtected = false, parentDirectory = undefined }) {
        /** @type {State<string>} */
        this._fileName = new State(fileName);

        /** @type {undefined | Directory} */
        this.parentDirectory = parentDirectory;

        /** @type {boolean} When true, the directory cannot be deleted */
        this._isProtected = isProtected;
    };

    getPath() {
        return this.parentDirectory.getPath();
    };

    /**
     * @param {string} fileName
     */
    renameFile(fileName) {
        this._fileName.setValue(fileName);
    };

    get fileName() {
        return this._fileName.getValue();
    };
};

class Group extends Identifiable {
    /**
     * 
     * @param {{
     *  groupName: string,
     *  groupItems: string
     * }}
     */
    constructor({ groupName, groupItems = [] }) {
        this.groupName = groupName;
        this.groupItems = groupItems;
    };
};

class Item extends Identifiable {
    /**
     * 
     * @param {{
     *  itemName: string,
     *  itemCaption: string
     * }}
     */
    constructor({ itemName, itemCaption = "" }) {
        this.itemName = itemName;
        this.itemCaption = itemCaption;
    };
};

class Menu extends Identifiable {
    constructor() {
        /** @type {Item[]} */
        this._items = [];
    };
};

/**
 * @global
 */
const Application = {
    Modules: new Registry(),

    Events: {

    },

    /**
     * Utility helper functions
     */
    Common: {
        /**
         * Generates a unique UUID
         * 
         * @returns {string}
         */
        UUID() {
            return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },

        /**
         * 
         * @param {string} HTMLString 
         * @returns {HTMLElement}
         */
        parseHTML(HTMLString) {
            const div = document.createElement("div");
            div.innerHTML = HTMLString;

            if (div.children.length !== 1) throw "Cannot parse multiple elements as single elements; wrap your `innerHTML` string in a div or another element.";

            return Array.from(div.children)[0]
        }
    },

    UI: {
        Elements: {
            /**
             * 
             * @param {{
             *  iconName: string
             * }} param0 
             */
            Icon(iconName) {
                const icon = document.createElement("i");
                icon.innerText = iconName;
                icon.setAttribute("icon", "");

                return icon;
            },
        },

        Regions: {
            Menus: {
                FileMenu: new FileMenu.Menu()
            }
        },

        /**
         * When the UI is refreshed, each callback in this list will be executed
         */
        UIDependencies: new SubscriptionList(),

        refreshUI() {}
    },

    FileSystem: new Directory("/", { isProtected: true, overridePath: ["/"], parentDirectory: "/" }),

    Document: {
        newDocument() {},

        openDocument() {},

        /** @type {State<Editor | undefined>} */
        activeDocument: new State(undefined)
    },

    Notification: {
        /**
         * @param {{
         *  message: string,
         *  title: string
         * }} param0 
         * @returns {Promise<boolean>}
         */
        createAlert({ message, title }) {
            return new Promise((resolve, reject) => {
                resolve(true);
            })
        },

        createDialog({ title, content }) {

        }
    },

    Types: {
        FileSystem: {
            File: File,
            Directory: Directory
        }, FileMenu: {
            Item: Item,
            Menu: Menu,
            Group: Group
        }, Identifiable: Identifiable
    }
};