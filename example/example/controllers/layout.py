from fastapi import Depends
from mountaineer import Metadata, RenderBase, LayoutControllerBase
from example.auth import AuthDependencies, UserOutput

class LayoutRender(RenderBase):
    user: UserOutput | None = None

class LayoutController(LayoutControllerBase):
    view_path = "src/pages/layout.tsx"

    async def render(self, user: UserOutput | None = Depends(AuthDependencies.get_user)) -> LayoutRender:
        return LayoutRender(
            user=user,
            metadata=Metadata(title="Home"),
        )