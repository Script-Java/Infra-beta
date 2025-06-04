import Link from "next/link";

export default function Home() {
  return (
    <div className="">
      <main className="">
        <p>Hello world</p>
        <div className="flex gap-4 mt-2">
          <Link href="/login" className="text-blue-600 underline">
            Login
          </Link>
          <Link href="/register" className="text-blue-600 underline">
            Register
          </Link>
        </div>
      </main>
    </div>
  );
}
