if (typeof firebase === 'undefined') throw new Error('hosting/init-error: Firebase SDK not detected. You must include it before /__/firebase/init.js');
var firebaseConfig = {
    apiKey: "AIzaSyBlzMgEY29htVUqNSIg8gO_i3ehPpxF3zg",
    authDomain: "videocalltest1-19928.firebaseapp.com",
    projectId: "videocalltest1-19928",
    storageBucket: "videocalltest1-19928.appspot.com",
    messagingSenderId: "265177188319",
    appId: "1:265177188319:web:51255aab53edd0a30ce66a",
    measurementId: "G-550G3HWJDX"
  };
if (firebaseConfig) {
  firebase.initializeApp(firebaseConfig);

  var firebaseEmulators = undefined;
  if (firebaseEmulators) {
    console.log("Automatically connecting Firebase SDKs to running emulators:");
    Object.keys(firebaseEmulators).forEach(function(key) {
      console.log('\t' + key + ': http://' +  firebaseEmulators[key].host + ':' + firebaseEmulators[key].port );
    });

    if (firebaseEmulators.database && typeof firebase.database === 'function') {
      firebase.database().useEmulator(firebaseEmulators.database.host, firebaseEmulators.database.port);
    }

    if (firebaseEmulators.firestore && typeof firebase.firestore === 'function') {
      firebase.firestore().useEmulator(firebaseEmulators.firestore.host, firebaseEmulators.firestore.port);
    }

    if (firebaseEmulators.functions && typeof firebase.functions === 'function') {
      firebase.functions().useEmulator(firebaseEmulators.functions.host, firebaseEmulators.functions.port);
    }

    if (firebaseEmulators.auth && typeof firebase.auth === 'function') {
      firebase.auth().useEmulator('http://' + firebaseEmulators.auth.host + ':' + firebaseEmulators.auth.port);
    }
  } else {
    console.log("To automatically connect the Firebase SDKs to running emulators, replace '/__/firebase/init.js' with '/__/firebase/init.js?useEmulator=true' in your index.html");
  }
}