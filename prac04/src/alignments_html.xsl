<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <xsl:output method="xhtml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <link href="alignments.css" rel="stylesheet" type="text/css"/>
                <title>
                    <xsl:value-of select="alignments/@name"/>
                </title>
            </head>
            <body>
                <table>
                    <xsl:apply-templates select="alignments/sequence-alignment"/>
                </table>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="sequence-alignment">
        <tbody class="alignment">
            <tr>
                <th class="desc">
                    <xsl:if test="@reading-frame">
                        <xsl:text>Frame: </xsl:text>
                        <xsl:value-of select="@reading-frame"/>
                        <xsl:text>;</xsl:text>
                    </xsl:if>
                    <xsl:value-of select="@matrix-name"/>
                </th>
                <xsl:for-each select="sequences/sequence[1]/node()">
                    <th>
                        <xsl:value-of select="floor((position() mod 1000) div 100)"/>
                    </th>
                </xsl:for-each>
            </tr>
            <tr>
                <th class="desc">penalty = <xsl:value-of select="@gap-penalty"/></th>
                <xsl:for-each select="sequences/sequence[1]/node()">
                    <th>
                        <xsl:value-of select="floor((position() mod 100) div 10)"/>
                    </th>
                </xsl:for-each>
            </tr>
            <tr>
                <th class="desc"><xsl:value-of select="count(.//GAP)"/> gaps.</th>
                <xsl:for-each select="sequences/sequence[1]/node()">
                    <th>
                        <xsl:value-of select="position() mod 10"/>
                    </th>
                </xsl:for-each>
            </tr>
            <xsl:for-each select="sequences/sequence">
                <tr class="alignment">
                    <td class="seq_name">
                        <xsl:value-of select="name"/>
                    </td>
                    <xsl:apply-templates select="node()[local-name() != 'name']"/>
                </tr>
            </xsl:for-each>
        </tbody>
    </xsl:template>

    <xsl:template match="GAP">
        <td class="gap alignment">-</td>
    </xsl:template>

    <xsl:template match="A[@codon = 'start']">
        <td class="atg_codon">A</td>
    </xsl:template>

    <xsl:template match="T[@codon = 'start']">
        <td class="atg_codon">T</td>
    </xsl:template>

    <xsl:template match="G[@codon = 'start']">
        <td class="atg_codon">G</td>
    </xsl:template>

    <xsl:template match="T[preceding-sibling::node()[1][@codon = 'start']]">
        <td class="atg_codon">T</td>
    </xsl:template>

    <xsl:template match="G[preceding-sibling::node()[2][@codon = 'start']]">
        <td class="atg_codon">G</td>
    </xsl:template>

    <xsl:template match="T[@codon = 'stop']">
        <td class="stop_codon">T</td>
    </xsl:template>

    <xsl:template match="A[preceding-sibling::node()[1][@codon = 'stop']]">
        <td class="stop_codon">A</td>
    </xsl:template>

    <xsl:template match="A[preceding-sibling::node()[2][@codon = 'stop']]">
        <td class="stop_codon">A</td>
    </xsl:template>

    <xsl:template match="G[preceding-sibling::node()[1][@codon = 'stop']]">
        <td class="stop_codon">G</td>
    </xsl:template>

    <xsl:template match="G[preceding-sibling::node()[2][@codon = 'stop']]">
        <td class="stop_codon">G</td>
    </xsl:template>
    
    <xsl:template match="M">
        <td class="atg_codon">M</td>
    </xsl:template>    

    <!-- fallback match of non-special letters -->
    <xsl:template match="A | B| C | D | E | F | G | H | I | J | K | L | N | O | P | Q | R | S| T | U | V | X | Y | Z">
        <td class="alignment">
            <xsl:value-of select="local-name()"/>
        </td>
    </xsl:template>

</xsl:stylesheet>
