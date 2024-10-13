// @ts-nocheck
import { json } from '@sveltejs/kit';
import { connectToDatabase } from '$lib/mongo.js';
import { ObjectId } from 'mongodb';



function ValidateData(data){

    
    const checks=["reactionTime","teamId","redness","pupils","heartBeats"];


    // THIS LOOP CHECKS IF THE DATA IS VALID FOR THE POST
    for (const element of checks) {
        
        if (!data[element] || typeof data[element] !== "number") {
            return false;
        }
    }

    return true;

}


export async function POST({request}) {
    try{

        
        const body = await request.json();// DATA
        
        if (!ValidateData(body)) {
            return json({ success: false, error: "BAD INPUT" }, { status: 400 });
        }

        const client = await connectToDatabase();
        const db = client.db('HOSPITAL');
        const collection = db.collection('DOCTOR');
        const result = await collection.insertOne(body);

        await client.close();

        return json({ success: true, insertedId: result.insertedId }, { status: 200 });
    }

    catch(error){
        console.error("ERROR WITH POST METHOD OF DOCTOR",error);
        return json({success:false,error: error.message},{status:500});
    }
  }

export async function GET({url}){

    try{ 

        const my_id = url.searchParams.get('id');

        if(my_id){
            
        

        let objectId;
        try {
            objectId = new ObjectId(my_id);
        } catch (error) {
            return json({ success: false, error: "Invalid ObjectId format" }, { status: 400 });
        }

        const client = await connectToDatabase();
        const db = client.db('HOSPITAL');
        const collection = db.collection('DOCTOR');
        const my_result = await collection.findOne({"_id":objectId});

        await client.close();


        if (!my_result) {
            return json({ success: false, error: "No data found for the provided ID" }, { status: 404 });
        }


    return new Response(JSON.stringify({ message: 'DATA RETRIEVED SUCCESSFULLY', result:my_result }), {status: 200});
    } // GET ALL DOCTORS IF NO ID WAS PROVIDED
    else{
        const client = await connectToDatabase();
            const db = client.db('HOSPITAL');
            const collection = db.collection('DOCTOR');
            const allDoctors = await collection.find({}).toArray(); 

            await client.close();

            return json({ success: true, result: allDoctors }, { status: 200 });
    }
    }
    catch (error){
        return json({success:false,error: error.message},{status:500})
    }
}