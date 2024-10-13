export async function GET() {
  return new Response(JSON.stringify({ message: 'Hello from the API using svelte and js server code!' }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json'
    }
  });
}