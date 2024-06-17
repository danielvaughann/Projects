<template>
  <div class="mt-4" >
    <h2>Welcome to Lazy Linker</h2>
    <form class="detail-box my-5">
      <div class="form-group my-3">
        <h4>Signup to Chat</h4>
        <input
            type="text"
            v-model="name"
            class="form-control mb-4 mt-4"
            placeholder="Enter your name..."
        />
        <input
            type="text"
            v-model="email"
            class="form-control mb-4"
            placeholder="Enter your email..."
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
            @click="signup"
            class="btn btn-primary"
        >Signup</button>
        <router-link :to="{ path: '/' }">
          <h6 class="mt-3" style="font-weight: 600">Back to login</h6>
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import firebase from "../api/firebase";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { getFirestore, collection, addDoc } from "firebase/firestore";
import { useRouter } from 'vue-router'; // Import useRouter from vue-router


export default {
  name: "Signup",
  data() {
    return {
      name: "",
      email: "",
      password: ""
    };
  },
  methods: {
    async signup() {
      const auth = getAuth(firebase);
      const firestore = getFirestore(firebase);
      const router = useRouter();



      try {
        //create user with email and password
        const userCredential = await createUserWithEmailAndPassword(
            auth,
            this.email,
            this.password
        );
        const user = userCredential.user;

        //add user to database
        await addDoc(collection(firestore, "users"), {
          name: this.name,
          email: this.email,
          URL: "",
          description: "",
          password: this.password,
          userId: user.uid
        });

        console.log("User signed up and added to database successfully");

        // Redirect to chat page after signup
        this.$router.push('/chat'); // Redirect to the chat page

      } catch (error) {
        console.error("Error signing up:", error);
        // Handle error (e.g., display error message to the user)
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
  border-color: #4f90ff; ]
}

</style>