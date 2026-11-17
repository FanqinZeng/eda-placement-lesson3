import { loadPyodide } from '../vendor/pyodide/pyodide.mjs';
import { MAX_OUTPUT_CHARS } from './examples.mjs';
let pyodide;
let activeRun = null;
let outputChars = 0;
let truncated = false;
function output(kind, text) {
  if (activeRun === null || truncated) return;
  const remaining = MAX_OUTPUT_CHARS - outputChars;
  const value = String(text).slice(0, remaining);
  outputChars += value.length;
  self.postMessage({type:'output', id:activeRun, kind, text:value});
  if (outputChars >= MAX_OUTPUT_CHARS) {
    truncated = true;
    self.postMessage({type:'output', id:activeRun, kind:'stderr', text:'[Output limit reached / 输出已达上限]\n'});
  }
}
try {
  pyodide = await loadPyodide({indexURL:new URL('../vendor/pyodide/', import.meta.url).href});
  for (const [kind, setter] of [['stdout', 'setStdout'], ['stderr', 'setStderr']]) {
    const decoder = new TextDecoder();
    pyodide[setter]({write:buffer => {output(kind, decoder.decode(buffer, {stream:true}));return buffer.length}});
  }
  self.postMessage({type:'ready', version:pyodide.runPython('import sys; sys.version.split()[0]')});
} catch (error) {
  self.postMessage({type:'init-error', error:String(error)});
}
self.onmessage = async ({data}) => {
  if (data.type !== 'run' || !pyodide || activeRun !== null) return;
  activeRun = data.id;
  outputChars = 0;
  truncated = false;
  const globals = pyodide.toPy({__name__:'__main__'});
  let result = {type:'done', id:data.id};
  try {
    await pyodide.runPythonAsync(data.code, {globals});
  } catch (error) {
    result = {type:'error', id:data.id, error:String(error)};
  } finally {
    // CPython buffers partial lines; flush before reporting the run as complete.
    try {pyodide.runPython('import sys; sys.stdout.flush(); sys.stderr.flush()')} catch {}
    self.postMessage(result);
    globals.destroy();
    activeRun = null;
  }
};
