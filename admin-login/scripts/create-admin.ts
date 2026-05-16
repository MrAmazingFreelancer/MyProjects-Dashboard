// scripts/create-admin.ts
// Run with: npx ts-node scripts/create-admin.ts
import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

async function main() {
  const email = "admin@7ink.com.au"; // Change this
  const password = "changeme123";     // Change this!
  const name = "Admin";

  const hashedPassword = await bcrypt.hash(password, 12);

  const user = await prisma.user.upsert({
    where: { email },
    update: {},
    create: {
      email,
      name,
      password: hashedPassword,
      role: "admin",
    },
  });

  console.log("✅ Admin user created:", user.email);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
