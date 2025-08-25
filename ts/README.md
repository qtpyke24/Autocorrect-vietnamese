# tạo project
mkdir my-ts-project && cd my-ts-project
npm init -y
npm install typescript @types/node --save-dev

# init tsconfig.json
npx tsc --init

# biên dịch
npx tsc

# chạy
node dist/index.js
