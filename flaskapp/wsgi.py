
from iz import app
if __name__ == "__main__":
  app.run()

app.get('/app/:id', doEverythingInOneHugeFunctionWithAsyncBranches);
  
app.get('/app/:id', checkUserAuth, findApp, renderView, sendJSON);

function checkUserAuth(req, res, next) {
 if (req.session.user) return next();
 return next(new NotAuthorizedError());
}
