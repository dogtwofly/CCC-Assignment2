    
// pride:

module.exports = {
    'GET /chart_pride': async (ctx, next) => {
            ctx.render('chart_pride.html', {
                title: 'COMP90024 TEAM18 ASSIGNMENT2',
                name: 'PRIDE'
            });
         
    }
};