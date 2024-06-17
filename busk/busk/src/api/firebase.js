import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries


// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCbpQ2UNNqpCm570Jo5Lh3nVyHCTKQUjWk",
    authDomain: "busk-b7b80.firebaseapp.com",
    projectId: "busk-b7b80",
    storageBucket: "busk-b7b80.appspot.com",
    messagingSenderId: "867748449830",
    appId: "1:867748449830:web:385cf1197769c9042720e7",
    measurementId: "G-0JDJ9X2ZSH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export default app;