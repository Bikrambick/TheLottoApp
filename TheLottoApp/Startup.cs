using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(TheLottoApp.Startup))]
namespace TheLottoApp
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
