import { MongoClient, Long } from 'mongodb';
import { json } from '@sveltejs/kit';

const uri = 'mongodb+srv://gilvaldezarreola:3p5d3XRxRmlGjoNx@cluster0.uyyqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
const client = new MongoClient(uri);

export async function GET({ url }) {
    const mid = url.searchParams.get('id');
    console.log(mid);

    try {
        await client.connect();
        const database = client.db('HOSPITAL');
        const collection = database.collection('HeartRate');

        if (!mid) {
            const ids = await collection.find({}, { projection: { id: 1 } }).toArray();
            const idList = ids.map(doc => doc.id ? doc.id.toString() : null).filter(id => id !== null);
            return json({ ids: idList }, { status: 200 });
        }

        const query = { id: Long.fromString(mid) };
        const result = await collection.findOne(query);

        if (!result) {
            return json({ error: 'No document found with the given ID' }, { status: 404 });
        }

        return json({ ans: result }, { status: 200 });
    } catch (error) {
        console.error(error);
        return json({ error: 'Internal Server Error' }, { status: 500 });
    } finally {
        await client.close();
    }
}