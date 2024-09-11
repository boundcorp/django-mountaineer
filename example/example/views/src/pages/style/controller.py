from mountaineer import Metadata, RenderBase
from django_mountaineer.controllers import PageController

class StyleRender(RenderBase):
    pass

# Need to wrap render in sync_to_async
class StyleController(PageController):
    def render( self ) -> StyleRender:
        return StyleRender(
            metadata=Metadata(title="Style"),
        )