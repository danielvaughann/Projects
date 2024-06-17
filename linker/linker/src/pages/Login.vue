<template>
  <div class="mt-4">
    <h2>Welcome to Lazy Linker</h2>

    <form class="detail-box my-5">
      <div class="form-group my-3">
        <h4>Login to Chat</h4>
        <input
            type="text"
            v-model="email"
            class="form-control mb-4"
            placeholder="Enter your email..."
            v-on:keyup.enter="login"
        />
        <input
            type="password"
            v-model="password"
            class="form-control mb-4"
            placeholder="Enter your password..."
        />

        <button
            style="font-weight: 600"
            type="button"
            @click="login"
            class="btn btn-primary"
        >Login</button>
        <router-link :to="{ path: '/signup' }">
          <h6 class="mt-3" style="font-weight: 600">Signup</h6>
        </router-link>
      </div>
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>
    </form>
  </div>
</template>
<script>
import firebase from "../api/firebase";
import { getFirestore, collection, query, where, getDocs } from "firebase/firestore";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { useRouter } from 'vue-router';


export default{
  firebase: "Login",
  data(){          //initialise variables
    return{
      email: "",
      password: "",
      errorMessage:""
    }
  },
  methods: {
    async login() {
      const auth = getAuth(firebase); //initialise firebase authentication
      const firestore = getFirestore(firebase); //initailise database
      const router = useRouter(); // Use useRouter to get the router instance

      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password); //built in sign in
        const user = userCredential.user;

        if (user) {
          console.log("Logged in !", user);
          const q = query(collection(firestore, 'users'), where('userId', '==', user.uid)); // fetches user information from database
          const querySnapshot = await getDocs(q);

          querySnapshot.forEach((doc) => { //iterates over results
            const userData = doc.data();
            localStorage.setItem("userId", userData.userId);
            localStorage.setItem("name", userData.name);
            localStorage.setItem("email", userData.email);
            localStorage.setItem("password", userData.password);
            localStorage.setItem("description", userData.description);
            localStorage.setItem("FirebaseDocumentId", doc.id);
          });

          this.errorMessage = ""; //error message empty
          console.log("Logging in")
           this.$router.push('/chat'); // Redirect to the chat page
        }
      } catch (error) {
        const errorMessage = "Email or password incorrect, please try again";
        console.error(error);
        this.errorMessage = errorMessage;
      }
    }
  }
};
</script>

<style>
input[type="text"],
input[type="password"] {
  margin: 0 auto;
  width: 80%;
  background-color: #65b5ff;
  border: 1px solid #65b5ff;
  border-radius: 5px;
  padding: 8px;
  color: #fff;
}
body {
  background-color: #87CEFA;
}
.detail-box {
  padding: 15px;
  border: 1px solid #2496ff;
  width: 400px;
  min-height: 250px;
  margin: 0 auto ;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2,
h4 {
  font-weight: 600;
}

h2 {
  margin-bottom: 20px;
}

h4 {
  margin-bottom: 15px;
}

.btn-primary {
  background-color: #6fc1ff;
  border-color: #6fc1ff;
  color: #fff;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 5px;
}

.btn-primary:hover {
  background-color: #4f90ff;
  border-color: #4f90ff;
}


</style>