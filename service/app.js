const Koa = require('koa');

const fs = require('fs');

const router = require('koa-router')();

const bodyParser = require('koa-bodyparser');

const controller = require('./controller');

const templating = require('./templating');

const app = new Koa();

const isProduction = process.env.NODE_ENV === 'production';

//add url-route:

router.get('/index.html', async (ctx, next) => {
    var name = ctx.params.name;
	ctx.response.type = 'html';
	ctx.response.body = fs.createReadStream('./views/index.html');
});

router.get('/aurin.html', async (ctx, next) => {
    var name = ctx.params.name;
	ctx.response.type = 'html';
	ctx.response.body = fs.createReadStream('./views/aurin.html');
});

router.get('/chart_lust.html', async (ctx, next) => {
    var name = ctx.params.name;
	ctx.response.type = 'html';
	ctx.response.body = fs.createReadStream('./views/chart_lust.html');
});

router.get('/chart_wrath.html', async (ctx, next) => {
    var name = ctx.params.name;
	ctx.response.type = 'html';
	ctx.response.body = fs.createReadStream('./views/chart_wrath.html');
});

router.get('/', async (ctx, next) => {
    ctx.response.body = '<h1>Index</h1>';
});


// log request URL:
app.use(async (ctx, next) => {
    console.log(`Process ${ctx.request.method} ${ctx.request.url}...`);
    var
        start = new Date().getTime(),
        execTime;
    await next();
    execTime = new Date().getTime() - start;
    ctx.response.set('X-Response-Time', `${execTime}ms`);
});

// static file support:
if (! isProduction) {
    let staticFiles = require('./static-files');
    app.use(staticFiles('/static/', __dirname + '/static'));
}

// parse request body:
app.use(bodyParser());

// add nunjucks as view:
app.use(templating('views', {
    noCache: !isProduction,
    watch: !isProduction
}));

// add controller:
app.use(controller());
app.use(router.routes());


app.listen(8080);
console.log('app started at port 8080...');