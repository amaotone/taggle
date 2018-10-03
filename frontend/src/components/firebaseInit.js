import firebase from 'firebase'
import 'firebase/firestore'
const firebaseApp = firebase.initializeApp({
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: 'taggle-8cd4d.firebaseapp.com',
  databaseURL: 'https://taggle-8cd4d.firebaseio.com',
  projectId: 'taggle-8cd4d',
  storageBucket: 'taggle-8cd4d.appspot.com',
  messagingSenderId: '181612162187'
})
export default firebaseApp.firestore()
