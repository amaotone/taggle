import Vue from 'vue'
import VueFirestore from 'vue-firestore'
import firebase from 'firebase/app'
import 'firebase/firestore'

Vue.use(VueFirestore)

var firebaseApp = firebase.initializeApp({
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: 'taggle-8cd4d.firebaseapp.com',
  databaseURL: 'https://taggle-8cd4d.firebaseio.com',
  projectId: 'taggle-8cd4d',
  storageBucket: 'taggle-8cd4d.appspot.com',
  messagingSenderId: '181612162187'
})
const firestore = firebaseApp.firestore()
firestore.settings({timestampsInSnapshots: true})
export default firestore
