import http from "http"
import express from "express"
import serveStatic from "serve-static"
import path from "path"

const app = express();
const __dirname = path.resolve();
const router = express.Router();

router.route('/').get((req,res)=>{
    res.redirect(`/webapp_test/todo.html`);
})

router.route('/home').get((req,res)=>{
    res.redirect(`/webapp_test/todo.html`);
})

router.route('/login').get((req,res)=>{
    res.redirect(`/webapp_test/login.html`);
})

app.use(serveStatic(`${__dirname}/..`));
app.use(`/`,router);
app.use(`/login`,router);
app.use(`/home`,router);

http.createServer(app).listen(5000,`127.0.0.1`);