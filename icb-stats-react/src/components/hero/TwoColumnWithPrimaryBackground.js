import React from "react";
import tw from "twin.macro";
import { css } from "styled-components/macro"; //eslint-disable-line
import HeaderBase, {
  LogoLink as LogoLinkBase,
  NavLinks,
  NavLink as NavLinkBase,
  PrimaryLink as PrimaryLinkBase
} from "../headers/light.js";
import { Container as ContainerBase, ContentWithVerticalPadding, Content2Xl } from "components/misc/Layouts.js";
import { SectionHeading } from "components/misc/Headings.js";
import { SectionDescription } from "components/misc/Typography.js";
import { PrimaryButton as PrimaryButtonBase } from "components/misc/Buttons.js";
import logoImageSrc from "images/hockeyplayer.png";
import serverIllustrationImageSrc from "images/server-illustration-2.svg";
import ReactTableGrid from "components/datagrid/ReactTableGrid";

const PrimaryBackgroundContainer = tw.div`-mx-8 px-8 bg-green-1000 text-cream-100`;
const Header = tw(HeaderBase)`max-w-none -mt-8 py-8 -mx-8 px-8`;
const NavLink = tw(NavLinkBase)`lg:text-cream-100 lg:hocus:text-black lg:hocus:border-black`;
const LogoLink = tw(LogoLinkBase)`text-cream-100 hocus:text-black`;
const PrimaryLink = tw(PrimaryLinkBase)`shadow-raised text-cream-100 hocus:text-cream-100 lg:bg-black lg:hocus:bg-green-800`;

const Container = tw(ContainerBase)``;
const Row = tw.div`flex items-center flex-col lg:flex-row`;
const Column = tw.div`lg:w-1/2`;
const TextColumn = tw.div`text-center lg:text-left`;
const IllustrationColumn = tw(Column)`mt-16 lg:mt-0 lg:ml-16`;
const Heading = tw(SectionHeading)`max-w-3xl lg:max-w-4xl lg:text-left leading-tight`;
const Description = tw(SectionDescription)`mt-4 max-w-2xl text-cream-100 lg:text-base mx-auto lg:mx-0`;
const PrimaryButton = tw(PrimaryButtonBase)`mt-8 text-sm sm:text-base px-6 py-5 sm:px-10 sm:py-5 text-cream-100 hocus:text-cream-100 bg-black inline-block hocus:bg-green-800`;
const Image = tw.img`w-144 ml-auto`

export default () => {
  const logoLink = (
    <LogoLink href="/">
      <img src={logoImageSrc} alt="Logo" />
      Fantasy Hockey Stats
    </LogoLink>
  );
  const navLinks = [
    <NavLinks key={1}>
      <NavLink href="#">About</NavLink>
      <NavLink href="#">Stats</NavLink>
      <NavLink href="#">Schedule</NavLink>
      <PrimaryLink href="#">Hockeyvite</PrimaryLink>
    </NavLinks>
  ];

  return (
    <PrimaryBackgroundContainer>
      <Content2Xl>
        <Header logoLink={logoLink} links={navLinks} />
        <Container>
          <ContentWithVerticalPadding>
            <Row>
              <TextColumn>
                <ReactTableGrid />
              </TextColumn>
            </Row>
          </ContentWithVerticalPadding>
        </Container>
      </Content2Xl>
    </PrimaryBackgroundContainer>
  );
};
