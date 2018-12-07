const Koa = require('koa');
var Router = require('koa-router');

const app = new Koa();
const PORT = 8082;
var router = new Router();

router
    .get('/', (ctx, next) => {
        ctx.body = 'Hello World!';
    })
app
    .use(router.routes())
    .use(router.allowedMethods());

router
    .get('/koa_backend', (ctx, res) => {
        ctx.body = ({ express: 'YOUR KOA BACKEND IS CONNECTED TO REACT' });
});
const server = app.listen(PORT, () => {
    console.log(`Server listening on port: ${PORT}`);
});

module.exports = server;
