import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web firebase's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDyguOhVlPLKwlnKpp4SKgn5fNM_NVy6zA",
    authDomain: "linker-6027f.firebasefirebase.com",
    projectId: "linker-6027f",
    storageBucket: "linker-6027f.firebasespot.com",
    messagingSenderId: "734901639496",
    appId: "1:734901639496:web:52de8e006ce1e7b462fb7d",
    measurementId: "G-079K0KHJ6R"
};

// Initialize Firebase
const firebase = initializeApp(firebaseConfig);
const analytics = getAnalytics(firebase);
const firestore = getFirestore(firebase);

export default firebase;
export { firestore }; // Export Firestore for use in other files

