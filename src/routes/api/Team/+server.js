// @ts-nocheck

import { json } from '@sveltejs/kit';
import { connectToDatabase } from '$lib/mongo';



export async function GET(){

    try{ 
        
        const client = await connectToDatabase();
        const db = client.db('HOSPITAL');
        const collection = db.collection('TEAM');
        const my_result = await collection.find({}, { projection: { id: 1 } }).toArray();
        


        await client.close();



        const teamIds = my_result.map(team => team.id);

        return json({result:teamIds});

    }
    catch (error){
        return json({success:false,error: error.message},{status:500})
    }
}