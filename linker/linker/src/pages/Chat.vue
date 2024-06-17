<template>
  <div style="display: flex; height: 100vh">

    <div class="sidebar" style="width: 30vw; ">
      <h5>Friends</h5>
      <div>
        <button type="button" class="btn btn-primary" v-on:click="logout">Logout</button>
      </div>


      <ul class="list-unstyled components">
        <li
            class="active mb-3"
            v-on:click="letsChat(item)"
            v-for="item in filteredUsers"
            :key="item.userId || item.id"
            v-show="item.userId !== currentUserId "
        >
          <h6 style="line-height: 2; font-weight: 600">{{ item.isGroup ? item.groupName : item.name }}</h6> <!-- if item is a group it returns group name else returns just name -->
        </li>
      </ul>
      <div>
        <button type="button" class="btn btn-secondary" v-on:click="showGroupModal = true">Create Group Chat</button>
      </div>


      <div v-if="showGroupModal" class="group-modal">
        <h5>Create Group Chat</h5>
        <h8>(Click the box on left of name,click your own name too,then refresh page)<br></h8>
        <input type="text" v-model="newGroupName" placeholder="Group Name" />
        <div>
          <label v-for="user in searchUsers" :key="user.userId || user.id"> <!-- search for user id in each object in search users array -->
            <input type="checkbox" v-model="selectedUsers" :value="user.userId" />
            {{ user.name }}
          </label>
        </div>
        <button type="button" class="btn btn-primary" v-on:click="createGroupChat(newGroupName, selectedUsers)">Create</button>
        <button type="button" class="btn btn-secondary" v-on:click="showGroupModal = false">Cancel</button>
      </div>
    </div>


    <div class="chatbox" style="flex: 1; display: flex; flex-direction: column; margin-left: 30vw">
      <header v-if="currentPeerUser"> <!-- display peer user name in header once a name has been chosen -->
        <div style="height: 60px; background: #bde0fe">
          <div class="header-name"style="font-size: 22px; font-weight: bold;" >{{ currentPeerUser ? currentPeerUser.name : '' }} </div>
        </div>
      </header>
      <div style="background: white; flex: 1; overflow-y: auto">
        <h2 class="welcome" v-if="!currentPeerUser">Click a name to begin chatting!</h2>
        <div class="text-outer">

          <div

              :class="item.idFrom === currentUserId ? 'idFrom' : 'idTo'"
              class="text-inner"
              v-for="item in listMessage"
              :key="item.id"
          > <!-- gives identifier to message objects -->
            <!-- assigns id to or from class based on currentPeerUser id -->
            <h2>{{ item.senderName }}</h2>
            <h6>{{ item.content }}</h6>
          </div>
        </div>
      </div>
      <footer v-if="currentPeerUser">
        <div style="min-height: 60px; background: #bde0fe;">
          <div style="display: flex; padding: 15px">
            <button type="button" class="btn btn-primary mr-2" v-on:click="sendMessage(inputValue)">Send</button>
            <button type="button" class="btn btn-secondary mr-2" v-on:click="handleLazyResponse()">Im feeling lazy</button>

            <input
                type="text"
                style="width: 70%; border: 1px solid transparent; border-radius: 4px; padding: 5px 10px; background-color:white ;color: black"
                class="mr-3"
                v-model="inputValue"
                v-on:keyup.enter="sendMessage(inputValue)"
            />
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import firebase from "../api/firebase";
import Chatbox from "./Chatbox.vue";

import openai from './useAI.js'
import { getAuth, signOut, onAuthStateChanged } from "firebase/auth";
import {where,getDocs, collection, getFirestore, addDoc, query, onSnapshot} from "firebase/firestore";
import moment from "moment";

export default {
  components: {
    Chatbox
  },
  data() {
    return {  //initialises variables
      currentUserName: localStorage.getItem("name"),
      currentUserId: localStorage.getItem("id"),
      currentPeerUser: null,
      searchUsers: [],
      selectedUsers:[],
      newGroupName:"",
      filteredUsers:[],
      inputValue:"",
      showGroupModal: false,
      listMessage: [],
      groupChatId: null,
    };
  },
  methods: {

  async createGroupChat(groupName, selectedUsers) {
      try {
        const groupDocRef = await addDoc(collection(getFirestore(), "Groups"), {
          name: this.newGroupName,
          members: this.selectedUsers
          //sk-proj-2JlaKGXsxjJClmoHAvEET3BlbkFJlyXmNSdAwYUt0urOCE79

        });
        await this.getUserList()
        // Set the groupChatId to the ID of the newly created group document
        this.groupChatId = groupDocRef.id;
        console.log("selected users",selectedUsers)
        console.log("Group created with ID: ", this.groupChatId);
        this.newGroupName = ""; //resests new group name
        this.selectedUsers = [];
        this.showGroupModal=false; //stops group modal displaying
      } catch (error) {
        console.error("Error creating group chat: ", error);
      }

    },
    async handleLazyResponse() {
      if (this.listMessage.length === 0) {
        console.log("No messages available");
        return;
      }

      const lastMessage = this.listMessage[this.listMessage.length - 1].content; //gets last message from array

      try {

        const completion = await openai.chat.completions.create({
          model: "gpt-3.5-turbo", //api call this chatgpt
          messages: [
            { role: "system", content: "any prompt you receive is a text message from my friend I'm too tired to reply to. So I want you to reply as me in a funny way." },
            { role: "user", content: lastMessage },
          ],
        });

        const output_text = completion.choices[0].message.content; //receives chatgpt response
        console.log("OpenAI API response:", output_text);
        await this.sendMessage(output_text) //sends chatgpt message to send message function
        return { text: output_text.trim() }; //returns response object
      } catch (error) {
        console.error("Error fetching response from OpenAI:", error);
      }
    },

    async filterUsers() { // retrieves groupchat current user is a member of
      const firestore = getFirestore(firebase);

      //clears the filterUsers array before re adding to it
      this.filteredUsers = [];

      //get the groups that the current user is a member of
      const userGroupsSnapshot = await getDocs(query(collection(firestore, "Groups"), where("members", "array-contains", this.currentUserId)));

      userGroupsSnapshot.forEach((doc) => {
        const groupData = doc.data();

        this.filteredUsers.push({
          groupName: groupData.name,
          isGroup: true,
          id: doc.id
        });
      });

      //adds other users to the filteredUsers array
      const usersSnapshot = await getDocs(collection(firestore, "users"));
      usersSnapshot.forEach((doc) => {
        const userData = doc.data();
        if (userData.id !== this.currentUserId) {
          this.filteredUsers.push({
            userId: userData.userId,
            name: userData.name,
            email: userData.email,
            isGroup: false,
            description: userData.description
          });
        }
      });

      console.log("Filtered Users:", this.filteredUsers);
    },
    letsChat(item) {
      this.filterUsers()
      if (item.isGroup) {
        //sets currentPeerUser to user which was clicked on
        this.currentPeerUser = { userId: item.id, name: item.groupName };

        this.getMessages();
      } else {
        this.currentPeerUser = { userId: item.userId, name: item.name, email: item.email, description: item.description };
      }
      console.log(this.currentPeerUser);
      this.getMessages();
    },

    async getMessages() {
      if (!this.currentPeerUser || !this.currentPeerUser.userId) {
        console.error("currentPeerUser or currentPeerUser.userId is undefined");
        return;
      }


      if (this.currentPeerUser.email === undefined) { //checks if currentPeerUser is a group by checking email field
        this.groupChatId = this.currentPeerUser.name //groupchats just have a name no other details
      }else{
        const names = [this.currentUserName, this.currentPeerUser.name].sort();//creates message collection  name sorting in alphabetical order. so its the same for both users
        this.groupChatId = names.join('');
      }
      console.log("Group name/chat",this.groupChatId)
      const messageCollection = this.currentPeerUser.isGroup //if user is a group it goes to correct collection path
          ? `Groups/${this.currentPeerUser.userId}/messages`
          : `Messages/${this.groupChatId}/texts`;

      const q = query(collection(getFirestore(), messageCollection));

      onSnapshot(q, (snapshot) => {
        const messages = snapshot.docs.map((doc) => doc.data());
        messages.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)); //sorts messages newest first
        this.listMessage = messages;
        console.log("Messages in listMessage:", this.listMessage);
      });
    },
    async sendMessage(content) {
      if (!content.trim()) return;

      if (!this.currentPeerUser || !this.currentPeerUser.userId) {
        console.error("currentPeerUser or currentPeerUser.userId is undefined");
        return;
      }
      if (this.currentPeerUser.email===undefined) {
        this.groupChatId = this.currentPeerUser.name
      }else{
        const names = [this.currentUserName, this.currentPeerUser.name].sort();
        this.groupChatId = names.join('');
      }
      const timestamp = moment().format("YYYY-MM-DD HH:mm:ss");

      const message = {
        id: timestamp,
        idFrom: this.currentUserId,
        idTo: this.currentPeerUser.userId,
        timestamp: timestamp,
        senderName: this.currentUserName,
        content: content.trim(),

      };
      const messageCollection = this.currentPeerUser.isGroup
          ? `Groups/${this.currentPeerUser.userId}/messages`
          : `Messages/${this.groupChatId}/texts`;

      try {
        await addDoc(collection(getFirestore(), messageCollection), message);
        this.inputValue = "";
      } catch (error) {
        console.error("Error sending message: ", error);
      }
      await this.getMessages();
      console.log("send messages chatbox");
      console.log("groupChatId:", this.groupChatId);
      console.log("me:", this.currentUserId);
      console.log("them id:", this.currentPeerUser.userId);
      console.log("them name:", this.currentPeerUser.name);
      console.log("me name:", this.currentUserName);
    },

    async getUserList() {
      const firestore = getFirestore(firebase);


      const usersSnapshot = await getDocs(collection(firestore, "users"));
      const users = [];
      usersSnapshot.forEach((doc) => {
        const userData = doc.data();
        if (userData.id !== this.currentUserId) {
          users.push({
            userId: userData.userId,
            name: userData.name,
            email: userData.email,
            isGroup: false,

            description: userData.description
          });
        }
      });


      const groupsSnapshot = await getDocs(collection(firestore, "Groups"));
      const groups = [];
      groupsSnapshot.forEach((doc) => {
        const groupData = doc.data();
        groups.push({
          groupName: groupData.name,
          isGroup: true,
          id: doc.id
        });
      });


      this.searchUsers = [...users, ...groups];//combines both arrays into searchUsers array
      console.log(this.searchUsers)

      console.log("Users and groups fetched successfully");
    },


    logout() {
      const auth = getAuth(firebase); //gets firebase authentication
      signOut(auth); //built in signout function
      this.currentUserId = null;
      this.currentPeerUser = null; //resets fields

      this.$router.push("/");
      localStorage.clear();
      console.log("signed out");
    },
    setUserDetails(user) {

      this.currentUserId = user.uid;
      if (!localStorage.getItem("userId")) {
        localStorage.setItem("id", user.uid);
        localStorage.setItem("name", user.name);
        localStorage.setItem("email", user.email);
        localStorage.setItem("description", user.description);
        console.log(user);

      }
      console.log("setuserdetails chat");
      console.log("Current User Name: ", this.currentUserName);
      console.log("Current User ID: ", this.currentUserId);
      console.log("Current User Email: ", user.email);
    }

  },
  created() { //runs when page is loaded
    const auth = getAuth(firebase);
    onAuthStateChanged(auth, (user) => {
      if (user) {

        this.setUserDetails(user);
        this.getUserList();
        this.filterUsers();
      } else {
        this.$router.push("/");
      }
    });
    console.log("created chat");
  },

};
</script>

<style>

.welcome {
   color: #635a5a;
   font-weight: 600;
   margin: 10px 0px 32px;
 }


.text-outer {
  display: flex;
  flex-direction: column;
}
.text-inner {
  padding: 10px 10px 2px;
  border-radius: 0.5rem;
  width: 20%;
}
.idFrom {
  background: teal;
  color: white;
  margin: 0% 0% 20px 70%;
}
.sidebar {
  height: 100vh;
  width: 200px;
  background-color: #4cc9f0 ;
  position: fixed;
  top: 0;
  left: 0;
  padding: 1rem;
  overflow-y: auto;
}
.idTo {
  background: lightcoral;
  color: white;
  font-size: 10px;
  margin: 0% 0% 20px 5%;
}

h2{
  color:black;
  font-size: 18px;
  font-family: "Yu Gothic UI",ui-serif;

  top: 0;
  left: 0;
  margin: 20px 0% 0% 0%;

}

h8{
  color: black;
  font-size: 11px;
}
.header-name{
  font-size: 50px;
  font-weight: bold;
}

</style>