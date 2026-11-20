"""Transcribe el crudo con tiempos por palabra (Whisper turbo; el modelo se baja de openaipublic.azureedge.net).
Uso:  python3 transcribir.py <crudo.mp4> <salida.json> "Marca, nombres propios, terminos"
El tercer argumento es el prompt inicial: ayuda con los nombres, pero igual revisar (en el 32 escribio "IMA" por IM8).
"""
import sys, json, subprocess, whisper
src, out = sys.argv[1], sys.argv[2]; prompt = sys.argv[3] if len(sys.argv) > 3 else None
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vn', '-ac', '1', '-ar', '16000', out + '.wav'], check=True)
r = whisper.load_model('turbo').transcribe(out + '.wav', language='es', word_timestamps=True, initial_prompt=prompt, verbose=None)
w = [{'w': x['word'].strip(), 's': round(x['start'], 2), 'e': round(x['end'], 2)} for s in r['segments'] for x in s['words']]
json.dump(w, open(out, 'w'), ensure_ascii=False)
for s in r['segments']: print('%.2f-%.2f %s' % (s['start'], s['end'], s['text']))
print(' '.join('%s@%.2f' % (x['w'], x['s']) for x in w))
