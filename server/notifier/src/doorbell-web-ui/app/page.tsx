import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "@/components/ui/navigation-menu"
import Link from "next/link"
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu"


export function Settings() {
  return (
    <div className="flex flex-col gap-[32px] items-center">
      <h1 className="text-2xl font-bold">Settings</h1>
      <p>Manage your account settings here.</p>
      <Button>Save Changes</Button>
    </div>
  );
}

export default function Home() {
  return (
    <div>
      <main>

        <NavigationMenu>
          <NavigationMenuList>
          <NavigationMenuItem>
          <Link href="/docs" legacyBehavior passHref>
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Documentation
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>

      </main>
      <footer>
        
      </footer>
    </div>
  );
}
