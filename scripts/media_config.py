"""Language-specific artifacts, keeping the original Chinese URLs stable."""
def media_config(lang):
    if lang not in ('zh','en'):raise ValueError('Unknown language: '+str(lang))
    suffix='' if lang=='zh' else '.en'
    return {'lang':lang,'voice':'zh-CN-XiaoxiaoNeural' if lang=='zh' else 'en-US-JennyNeural',
        'audio_dir':'video/audio' if lang=='zh' else 'video/audio/en',
        'story':'video/story.json' if lang=='zh' else 'video/story.en.json',
        'timeline':f'video/timeline{suffix}.json','video':f'lesson.{lang}.mp4',
        'captions':f'lesson.{lang}.vtt','chapters':f'chapters{suffix}.json','poster':f'poster{suffix}.jpg',
        'transcript':f'transcript{suffix}.md','report':f'media{suffix}.json'}
