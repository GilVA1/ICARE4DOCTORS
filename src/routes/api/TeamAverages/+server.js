// @ts-nocheck

import { connectToDatabase } from "$lib/mongo";
import { json } from "@sveltejs/kit";

// GET THE AVERAGE METRICS FOR A SINGLE TEAM
export async function GET({url}){
        try {

        var my_team = Number(url.searchParams.get('teamId'));
        


        const client = await connectToDatabase();
        
        var collection = client.db('HOSPITAL').collection('TEAM');


        const t_name = await collection.findOne({ "id": my_team }, { projection: { "name": 1 } });

        const department=t_name.name;
        

        // Get an array of Doctors with the corresponding team id
        collection = client.db('HOSPITAL').collection('DOCTOR');

        const my_result = await collection.find({"teamId": my_team}).toArray();

        await client.close();

        let sums={"reactionTime":0,"redness":0,"pupils":0,"heartBeats":0}
        for (const doctor of my_result){
            
            for(const key in sums ){
                if (key in sums){
                sums[key]+=doctor[key];
                }
            }
        }

        const doctorCount = my_result.length;
        for (const key in sums) {
            if (doctorCount > 0) {
                sums[key] = sums[key] / doctorCount;
            } else {
                sums[key] = 0; 
            }
        }

        
        sums.teamId=my_team;
        sums.name=department;


        return json({success:true,result:sums},{status:200})
        }
        catch (error){
            
            return json({success:false,error:error.message},{status:500})
        }
}