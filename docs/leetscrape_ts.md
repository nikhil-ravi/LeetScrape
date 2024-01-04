# LeetScrape TS

You can use the [leetscrape-ts](https://github.com/nikhil-ravi/leetscrape-ts) Next.js template to serve your solutions on the web. See the [demo](https://scuffedcode.chowkabhara.com/). Visit the repo for more details. You can generate the project using the `leetscrape ts` command:

```bash
leetscrape ts --out ./ts
```
This will bootstrap the project in the given directory. Follow the instructions in the [README](https://github.com/nikhil-ravi/leetscrape-ts/blob/main/README.md) and create/modify the `.env.local` file. Then, run the following command to generate the mdx files:

```bash
leetscrape solution --out ./ts/src/content/solutions ./solutions
```

You can then run the project using the following command:

=== "npm"
    ```bash
    cd ./ts
    npm run dev
    ```
=== "yarn"
    ```bash
    cd ./ts
    yarn dev
    ```
=== "pnpm"
    ```bash
    cd ./ts
    pnpm dev
    ```
=== "bun"
    ```bash
    cd ./ts
    bun dev
    ```