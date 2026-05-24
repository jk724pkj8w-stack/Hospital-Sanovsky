// src/firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCoUDMMFZCjgezR792UR5PqpZek942foK4",
  authDomain: "hospital-sanosvky-19c12.firebaseapp.com",
  projectId: "hospital-sanosvky-19c12",
  storageBucket: "hospital-sanosvky-19c12.firebasestorage.app",
  messagingSenderId: "106705125175",
  appId: "1:106705125175:web:383cebaaebce16002924b2",
  measurementId: "G-QZGHS427VV"
};

const app = initializeApp(firebaseConfig);

if (!app) {
  console.error('Firebase no se pudo inicializar');
} else {
  console.log('Firebase inicializado correctamente');
}

const db = getFirestore(app);
const auth = getAuth(app);

export { db, auth }; 