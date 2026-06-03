/**
 * KnotTales - Simulated Database Module
 * Acts as a central data store and connection layer.
 */

const DB_NAME = 'knottales_db_v1';

const db = {
    // Simulated "Connection"
    connect: function () {
        console.log('Connecting to KnotTales Database...');
        if (!localStorage.getItem(DB_NAME)) {
            this.seed();
        }
        console.log('Connected successfully.');
        return true;
    },

    // Seed initial data
    seed: function () {
        const initialData = {
            users: [],
            vendors: [
                { id: 1, name: 'The Taj Palace', category: 'venue', location: 'mumbai', rating: 4.9, price: '₹₹₹₹' },
                { id: 2, name: 'Royal Feasts', category: 'catering', location: 'delhi', rating: 4.8, price: '₹₹' },
                { id: 3, name: 'Stories by Nivedh', category: 'photography', location: 'bangalore', rating: 5.0, price: '₹₹₹' }
            ],
            bookings: [],
            tasks: [
                { id: 1, text: 'Finalize guest list', completed: false, priority: 'high' },
                { id: 2, text: 'Book venue', completed: true, priority: 'high' },
                { id: 3, text: 'Send invitations', completed: false, priority: 'medium' }
            ]
        };
        localStorage.setItem(DB_NAME, JSON.stringify(initialData));
    },

    // Get all data
    getData: function () {
        return JSON.parse(localStorage.getItem(DB_NAME));
    },

    // Save all data
    saveData: function (data) {
        localStorage.setItem(DB_NAME, JSON.stringify(data));
    },

    // User Operations
    createUser: function (user) {
        const data = this.getData();
        user.id = Date.now();
        data.users.push(user);
        this.saveData(data);
        return user;
    },

    findUser: function (email) {
        const data = this.getData();
        return data.users.find(u => u.email === email);
    },

    // Task Operations
    getTasks: function () {
        return this.getData().tasks;
    },

    toggleTask: function (taskId) {
        const data = this.getData();
        const task = data.tasks.find(t => t.id === taskId);
        if (task) {
            task.completed = !task.completed;
            this.saveData(data);
        }
    }
};

// Initialize DB on load
db.connect();

// Expose to window for use in pages
window.db = db;
