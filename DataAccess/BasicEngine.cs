using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using IronPython;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;

namespace DataAccess
{
    public class BasicEngine
    {
        private ScriptEngine engine;
        private ScriptScope scope;
        private ScriptSource source;
        private CompiledCode compiled;
        private object pythonClass;
        public BasicEngine(string pathToLib, string pathToPythonFile, string lottoId, string filePathHistory)
        {
            //creating engine and stuff
            engine = Python.CreateEngine();
            var paths = engine.GetSearchPaths();
            paths.Add(pathToLib);
            engine.SetSearchPaths(paths);
            //source = engine.CreateScriptSourceFromString("from math import sqrt" + Environment.NewLine + code, Microsoft.Scripting.SourceCodeKind.AutoDetect);
            scope = engine.CreateScope();

            string pyFileLoc = pathToPythonFile;
            source = engine.CreateScriptSourceFromFile(pyFileLoc);
            //loading and compiling code
            //source = engine.CreateScriptSourceFromString(code, Microsoft.Scripting.SourceCodeKind.Statements);
            try
            {
                compiled = source.Compile();

                compiled.Execute(scope);
            }
            catch (Exception ex) { var error = ex.Message.ToString(); }
            //now creating an object that could be used to access the stuff inside a python script
            try
            {
                pythonClass = engine.Operations.Invoke(scope.GetVariable("get_the_basic_engine"));
            }
            catch (Exception ex) { }
        }
        public dynamic CallFunction(string method, params dynamic[] arguments)
        {
            return engine.Operations.InvokeMember(pythonClass, method, arguments);
        }
    }
}
