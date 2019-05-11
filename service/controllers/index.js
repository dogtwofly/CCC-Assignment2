    
// index:

module.exports = {
    'GET /': async (ctx, next) => {
        ctx.render('index.html', {
            title: 'COMP90024 TEAM18 ASSIGNMENT2'
        });
    }
};