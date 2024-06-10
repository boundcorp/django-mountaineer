from mountaineer import ControllerBase, Metadata, RenderBase


class HomeRender(RenderBase):
    pass


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

    async def render(
        self,
    ) -> HomeRender:
        return HomeRender(
            items=[],
            metadata=Metadata(title="Home"),
        )
