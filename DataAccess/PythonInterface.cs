using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using IronPython;
using Microsoft.Scripting.Hosting;

namespace DataAccess
{
    /// <summary>
    /// This is where we write functions that talks to python application and returns data to our web project/browser.
    /// </summary>
    public class PythonInterface
    {
        private ScriptEngine engine;
        private ScriptScope scope;
        private ScriptSource source;
        private CompiledCode compiled;
        private object pythonClass;

        public PythonInterface(string pathToLib, string pathToPythonFile)
        {
            //Below are dummy data but useful, extracted from some other similar project


            ////creating engine and stuff
            //engine = Python.CreateEngine();
            //var paths = engine.GetSearchPaths();
            //paths.Add(pathToLib);
            //engine.SetSearchPaths(paths);
            ////source = engine.CreateScriptSourceFromString("from math import sqrt" + Environment.NewLine + code, Microsoft.Scripting.SourceCodeKind.AutoDetect);
            //scope = engine.CreateScope();
            
            //string pyFileLoc = pathToPythonFile;
            //source = engine.CreateScriptSourceFromFile(pyFileLoc);
            ////loading and compiling code
            ////source = engine.CreateScriptSourceFromString(code, Microsoft.Scripting.SourceCodeKind.Statements);
            //try
            //{
            //    compiled = source.Compile();

            //    compiled.Execute(scope);
            //}
            //catch (Exception ex) { var error = ex.Message.ToString(); }
            ////now creating an object that could be used to access the stuff inside a python script
            //pythonClass = engine.Operations.Invoke(scope.GetVariable("RunningCalculator"));
        }


    }
}
