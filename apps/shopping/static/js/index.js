"use strict";

// This will be the object that will contain the Vue attributes and be used to initialize it.
let app = {};

app.data = {
    items: [],       // Array to store items fetched from the server
    newItem: ''      // Holds the text of the new item to add
};

app.methods = {
    // Load items from the server
    loadItems() {
        fetch(load_data_url)
            .then(response => response.json())
            .then(data => {
                this.items = data.items;
            });
    },
    // Add a new item to the list
    addItem() {
        if (this.newItem.trim() === '') return;  // Ensure item is non-empty
        fetch(add_item_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_name: this.newItem })
        })
        .then(() => {
            this.newItem = '';  // Clear the input field after adding
            this.loadItems();    // Reload the list to show the new item
        });
    },
    // Toggle the purchased status of an item
    togglePurchased(itemId) {
        fetch(`${mark_purchased_url}/${itemId}`, { method: 'POST' })
            .then(() => this.loadItems());  // Reload the list to update item order
    },
    // Delete an item from the list
    deleteItem(itemId) {
        fetch(`${delete_item_url}/${itemId}`, { method: 'POST' })
            .then(() => this.loadItems());  // Reload the list to remove the deleted item
    }
};

// Vue instance
app.vue = Vue.createApp({
    data() {
        return app.data;
    },
    computed: {
        // Sort items so unchecked items appear at the top
        sortedItems() {
            return this.items.sort((a, b) => a.purchased - b.purchased);
        }
    },
    methods: app.methods,
    mounted() {
        this.loadItems();  // Initial data load when the app mounts
    }
}).mount("#app");
