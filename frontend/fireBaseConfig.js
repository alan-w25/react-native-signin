import firebase from "firebase/app";
import "firebase/auth";
import "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAyTT0GqV-dGb9cvzQKOQmu-gT86ZDk7_U",
  authDomain: "react-native-signin-9eaf0.firebaseapp.com",
  databaseURL: "https://react-native-signin-9eaf0.firebaseio.com",
  projectId: "react-native-signin-9eaf0",
  storageBucket: "react-native-signin-9eaf0.appspot.com",
  messagingSenderId: "99792931755",
};

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export { firebase };
