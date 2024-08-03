from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from mountaineer import Metadata, RenderBase, LayoutControllerBase, sideeffect
from example.auth import AuthDependencies, UserOutput
from django.contrib.auth import alogout

class LayoutRender(RenderBase):
    user: UserOutput | None = None

class LayoutController(LayoutControllerBase):
    view_path = "src/pages/layout.tsx"

    def render(self, user: UserOutput | None = Depends(AuthDependencies.get_user)) -> LayoutRender:
        return LayoutRender(
            user=user,
            metadata=Metadata(title="Home"),
        )

    @sideeffect
    async def logout(self, request: Request):
        await alogout(request.state.django_request)
        return RedirectResponse(url="/login")