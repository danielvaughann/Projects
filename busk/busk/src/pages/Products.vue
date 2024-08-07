<template>
  <div>
    <h1>Products</h1>
    <div class="products">
      <div v-for="(product, index) in products" :key="index" class="product-card">
        <h3>{{ product.name }}</h3>
        <div class="cost">{{ product.price }}</div>
        <!-- Changed from <img> to a <div> for the background image approach -->
        <div class="product-image" :style="{ backgroundImage: `url(${product.image})` }"></div>
        <button @click="addItemToCart(product)">Add to cart</button>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import guinness from "@/assets/Drinks/guinness.png";
import heineken from "@/assets/Drinks/heineken.png";
import carlsberg from "@/assets/Drinks/carlsbergpint.png";
import coors from "@/assets/Drinks/coors.png";
import corona from "@/assets/Drinks/corona.png";
import harp from "@/assets/Drinks/harp.png";
//import rockshore from "@/assets/Drinks/rockshore.png";
import moretti from "@/assets/Drinks/moretti.png";
import asahii from "@/assets/Drinks/asahii.png";
//import orchardthieves from "@/assets/Drinks/orchardthieves.png";
import vodka from "@/assets/Drinks/vodka.png";
import gin from "@/assets/Drinks/gin.png";
import whisky from "@/assets/Drinks/whisky.png";
import softdrink from "@/assets/Drinks/softdrink.png";
import dash from "@/assets/Drinks/dash.png";

export default {
  data() {
    return {
      products: [
        {
          name: "Guinness",
          price: "€5.10",
          image: guinness,
        },
        {
          name: "Heineken",
          price: "€6.20",
          image: heineken,
        },

        {
          name: "Coors",
          price: "€6.00",
          image: coors,
        },
        {
          name: "Corona",
          price: "€4.90",
          image: corona,
        },
        {
          name: "Harp",
          price: "€5.80",
          image: harp,
        },

        {
          name: "Moretti",
          price: "€6.90",
          image: moretti,
        },
        {
          name: "Asahii",
          price: "€7.00",
          image: asahii,
        },


        {
          name: "Vodka",
          price: "€5.50",
          image: vodka,
        },
        {
          name: "Gin",
          price: "€6.20",
          image: gin,
        },
        {
          name: "Whisky",
          price: "€7.30",
          image: whisky,
        },
        {
          name: "Soft Drink",
          price: "€1.90",
          image: softdrink,
        },
        {
          name: "Dash",
          price: "€0.50",
          image: dash,
        },
      ],
      customerKey: null // Initialize customerKey for the component
    };
  },
  mounted() {
    // Generate the customer key here when the component is mounted
    this.generateCustomerKey();
  },
  methods: {
    generateCustomerKey() {
      const min = 100; // Minimum value for a 3-digit number
      const max = 999; // Maximum value for a 3-digit number
      this.customerKey = String(Math.floor(Math.random() * (max - min + 1)) + min); // Generate a random number between min and max
    },
    addItemToCart(product) {
      const user = getAuth().currentUser;
      if (user) {
        const customerKey = this.customerKey; // Use the same customerKey for all items
        // Emit the event to add the product to the cart along with the customer key
        this.$emit("addItemToCart", { ...product, customerKey });
      } else {
        console.error("User not authenticated.");
      }
    }
  }
};
</script>

<style scoped>
body {
  margin: 0;
  font-family: 'Helvetica Neue', sans-serif;
  background-color: #191C23;
  color: #E9B464;
}

.products {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px; /* Increased gap for better spacing */
  padding: 40px; /* More padding for a spacious look */
}

.product-card {
  background: linear-gradient(145deg, #1E2029, #23252D); /* Subtle gradient for depth */
  border: 1px solid #3D4148;
  box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); /* Soft shadow for 3D effect */
  border-radius: 10px; /* Rounded corners for modern look */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 220px; /* Slightly larger cards */
  transition: transform 0.2s ease, box-shadow 0.2s ease; /* Smooth transitions for hover effects */
}

.product-card:hover {
  transform: translateY(-5px); /* Lift card on hover */
  box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.6); /* Enhance shadow on hover */
}

h1 {
  text-align: center;
  color: #E9B464;
  font-size: 2.5rem;
  margin-top: 20px;
  margin-bottom: 20px;
}

h3 {
  color: #E9B464;
  font-size: 1.4rem; /* Slightly larger for emphasis */
  margin-top: 15px;
  margin-bottom: 10px;
}

.cost {
  color: #A5763E;
  font-size: 1.1rem; /* Slightly larger for visibility */
  font-weight: bold;
  margin-bottom: 15px;
}

.product-image {
  width: 100%;
  height: 180px; /* Increased height for better display */
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-bottom: 2px solid #3D4148; /* Thicker border for separation */
}

button {
  background-color: #6D4F4B;
  color: #EDC9AF;
  border: none;
  padding: 12px 24px; /* More padding for larger button */
  font-weight: bold;
  width: calc(100% - 48px); /* Adjusted for new padding */
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  margin-bottom: 20px; /* Increased spacing */
}

button:hover {
  background-color: #D5954E;
  transform: scale(1.05); /* Button grows slightly */
}
</style>