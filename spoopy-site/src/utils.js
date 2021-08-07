export function storageAvailable(type) {
  let storage;
  try {
    storage = window[type];
    const x = "__storage_test__";
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    return (
      e instanceof DOMException &&
      // everything except Firefox
      (e.code === 22 ||
        // Firefox
        e.code === 1014 ||
        // test name field too, because code might not be present
        // everything except Firefox
        e.name === "QuotaExceededError" ||
        // Firefox
        e.name === "NS_ERROR_DOM_QUOTA_REACHED") &&
      // acknowledge QuotaExceededError only if there's something already stored
      storage &&
      storage.length !== 0
    );
  }
}

/**
 * @param {String} key The key to check with
 * @param {Boolean} value The value in case there isn't a key/LS
 * @returns {[Boolean, Boolean]} Returns Value & if it used the LS
 */
export function getKeyWrapper(key, value) {
  const trans = {
    1: true,
    2: false,
    3: "automated",
  };

  // If I can use LS then use it
  if (storageAvailable("localStorage")) {
    const keyCheck = localStorage.getItem(key);
    // If it is automated
    if (keyCheck === "3") {
      return [value, false];
    } else if (Object.keys(trans).includes(keyCheck)) {
      // Return the fetched value as something useful
      return [trans[keyCheck], true];
    }
    // If key not in DB
    console.warn(`Setting key for ${key}`);
    if (storageAvailable("localStorage")) {
      localStorage.setItem(key, "3");
    }
    return [value, false];
  }
  // Can't use LS, have whatever I'm given
  return [value, false];
}
