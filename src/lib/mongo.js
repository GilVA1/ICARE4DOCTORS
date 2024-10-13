// src/lib/mongodb.js
import { MongoClient } from 'mongodb';

const uri = 'mongodb+srv://gilvaldezarreola:3p5d3XRxRmlGjoNx@cluster0.uyyqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'; // Replace with your MongoDB URI
const client = new MongoClient(uri);

export async function connectToDatabase() {
    try {
        await client.connect();
        //console.log("Connected to MongoDB");
        return client;
    } catch (error) {
        console.error("Error connecting to MongoDB:", error);
        throw error;
    }
}

export async function closeDatabaseConnection() {
    await client.close();
    console.log("Connection to MongoDB closed");
}

connectToDatabase()
//setTimeout(() => {console.log("hey")},7000)
//closeDatabaseConnection()