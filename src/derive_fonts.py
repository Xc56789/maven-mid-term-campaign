"""Optional: regenerate bundled static fonts (pip install fonttools==4.66.1)."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

root=Path(__file__).resolve().parent.parent/'assets/fonts'
for weight,style in [(400,'Regular'),(700,'Bold')]:
    font=instantiateVariableFont(TTFont(str(root/'NotoSansSC-variable.ttf')),{'wght':weight},inplace=True)
    for platform,encoding,language in [(3,1,0x409),(1,0,0)]:
        for name_id,value in [(1,'MavenCampaignSans'),(2,style),(4,'MavenCampaignSans '+style),(6,'MavenCampaignSans-'+style),(16,'MavenCampaignSans'),(17,style)]:
            font['name'].setName(value,name_id,platform,encoding,language)
    target=root/('MavenCampaignSans-'+style+'.ttf')
    font.save(str(target))
    print('Saved',target.name)
